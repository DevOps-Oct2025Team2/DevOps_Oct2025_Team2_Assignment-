from io import BytesIO # BytesIO (a fake file that lives in memory)

def test_upload_route_unauthorised_returns_401(client):
    resp = client.post("/dashboard/upload")
    assert resp.status_code == 401

def test_upload_route_missing_file_returns_400(client):
    resp = client.post("/dashboard/upload", headers={"X-User-Id": "1"})
    assert resp.status_code == 400

def test_upload_route_success_returns_201_and_json(app, client, tmp_path):
    # Force upload dir to be tmp_path (so tests don't write into real folders)
    # Override upload config for test safety
    app.config["UPLOAD_DIR"] = str(tmp_path)
    app.config["MAX_UPLOAD_SIZE_BYTES"] = 1024
    app.config["ALLOWED_CONTENT_TYPES"] = {"text/plain"}

    # Build a fake multip part upload
    data = {
        "file" : (BytesIO(b"hello world"), "a.txt")
    }

    # Call route
    resp = client.post(
        "/dashboard/upload",
        data=data,
        headers={"X-User-Id": "1"},
        content_type="multipart/form-data",
    )

    # Assert HTTP Result
    assert resp.status_code == 201
    payload = resp.get_json()

    # Assert JSON Shape + content
    assert "file" in payload
    f = payload["file"]
    assert f["filename"] == "a.txt"
    assert f["content_type"] == "text/plain"
    assert f["size_bytes"] == 11

    # storage_path should point into our temp folder
    assert f["storage_path"].startswith(str(tmp_path))
    