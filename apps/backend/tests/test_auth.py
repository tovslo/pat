"""Tests for /api/v1/auth endpoints."""

from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.core.security import create_email_token, hash_password
from app.models.user import User

# ── helpers ──────────────────────────────────────────────────────────────────


async def _create_verified_user(db_session, email="user@example.com", password="password123"):
    user = User(email=email, hashed_password=hash_password(password), is_verified=True)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def _create_unverified_user(
    db_session, email="unverified@example.com", password="password123"
):
    user = User(email=email, hashed_password=hash_password(password), is_verified=False)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


def _register_data(email: str, password: str):
    return {"data": {"email": email, "password": password}}


# ── register ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    with patch("app.api.v1.auth.send_verification_email") as mock_task:
        mock_task.delay = lambda *a, **kw: None
        resp = await client.post(
            "/api/v1/auth/register",
            data={"email": "new@example.com", "password": "securepassword"},
        )
    assert resp.status_code == 201
    assert "подтвержден" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db_session):
    await _create_verified_user(db_session, "dup@example.com")
    with patch("app.api.v1.auth.send_verification_email") as mock_task:
        mock_task.delay = lambda *a, **kw: None
        resp = await client.post(
            "/api/v1/auth/register",
            data={"email": "dup@example.com", "password": "securepassword"},
        )
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_register_short_password(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/register",
        data={"email": "short@example.com", "password": "abc"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/register",
        data={"email": "not-an-email", "password": "password123"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_register_with_avatar(client: AsyncClient):
    minimal_png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
        b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        b"\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with (
        patch("app.api.v1.auth.send_verification_email") as mock_task,
        patch("app.api.v1.auth.upload_avatar", new_callable=AsyncMock) as mock_upload,
    ):
        mock_task.delay = lambda *a, **kw: None
        mock_upload.return_value = "http://localhost:9000/myapp-dev/public/avatars/test.png"
        resp = await client.post(
            "/api/v1/auth/register",
            data={"email": "avatar@example.com", "password": "securepassword"},
            files={"avatar": ("avatar.png", BytesIO(minimal_png), "image/png")},
        )
    assert resp.status_code == 201


# ── login ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session):
    await _create_verified_user(db_session)
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "password123",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "user@example.com"
    assert body["isVerified"] is True
    assert "avatarUrl" in body
    assert "access_token" in resp.cookies


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, db_session):
    await _create_verified_user(db_session)
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrong",
        },
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_unverified_returns_403(client: AsyncClient, db_session):
    await _create_unverified_user(db_session)
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "unverified@example.com",
            "password": "password123",
        },
    )
    assert resp.status_code == 403
    assert "не подтверждён" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login_unknown_email(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "ghost@example.com",
            "password": "password123",
        },
    )
    assert resp.status_code == 401


# ── verify-email ──────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_verify_email_success(client: AsyncClient, db_session):
    await _create_unverified_user(db_session, "noverify@example.com")
    token = create_email_token("noverify@example.com")
    resp = await client.post("/api/v1/auth/verify-email", json={"token": token})
    assert resp.status_code == 200
    assert "подтверждён" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_verify_email_invalid_token(client: AsyncClient):
    resp = await client.post("/api/v1/auth/verify-email", json={"token": "garbage.token.here"})
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_verify_email_already_verified(client: AsyncClient, db_session):
    await _create_verified_user(db_session, "already@example.com")
    token = create_email_token("already@example.com")
    resp = await client.post("/api/v1/auth/verify-email", json={"token": token})
    assert resp.status_code == 200


# ── me & logout ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_me_authenticated(client: AsyncClient, db_session):
    await _create_verified_user(db_session)
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "password123",
        },
    )
    assert login_resp.status_code == 200

    me_resp = await client.get("/api/v1/auth/me")
    assert me_resp.status_code == 200
    body = me_resp.json()
    assert body["email"] == "user@example.com"
    assert "avatarUrl" in body


@pytest.mark.asyncio
async def test_me_unauthenticated(client: AsyncClient):
    resp = await client.get("/api/v1/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_logout_clears_cookie(client: AsyncClient, db_session):
    await _create_verified_user(db_session)
    await client.post(
        "/api/v1/auth/login",
        json={
            "email": "user@example.com",
            "password": "password123",
        },
    )
    resp = await client.post("/api/v1/auth/logout")
    assert resp.status_code == 200
    me_resp = await client.get("/api/v1/auth/me")
    assert me_resp.status_code == 401


# ── avatar upload ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_avatar_authenticated(client: AsyncClient, db_session):
    await _create_verified_user(db_session)
    await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    minimal_png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00"
        b"\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    with patch("app.api.v1.auth.upload_avatar", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = "http://localhost:9000/myapp-dev/public/avatars/test.png"
        resp = await client.post(
            "/api/v1/auth/avatar",
            files={"avatar": ("avatar.png", BytesIO(minimal_png), "image/png")},
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["avatarUrl"] == "http://localhost:9000/myapp-dev/public/avatars/test.png"


@pytest.mark.asyncio
async def test_update_avatar_unauthenticated(client: AsyncClient):
    minimal_png = b"\x89PNG\r\n\x1a\n"
    resp = await client.post(
        "/api/v1/auth/avatar",
        files={"avatar": ("avatar.png", BytesIO(minimal_png), "image/png")},
    )
    assert resp.status_code == 401
