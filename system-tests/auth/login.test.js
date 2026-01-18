const axios = require("axios");

// Test case for successful login ( AC-LOGIN-01 )
describe("AC-LOGIN-01 — Successful Login", () => {
  it("should authenticate user and return JWT token and role", async () => {
    const response = await axios.post(
      "http://127.0.0.1:5000/api/login", // auth-service port
      {
        username: "user1",
        password: "user123"
      }
    );

    // HTTP success
    expect(response.status).toBe(200);

    // Token checks
    expect(response.data).toBeDefined();
    expect(response.data.access_token).toBeDefined();
    expect(response.data.token_type).toBe("Bearer");

    // Role-based logic
    expect(["admin", "user"]).toContain(response.data.role);
  });
});


// Test case for failed login ( AC-LOGIN-02 )
describe("AC-LOGIN-02 — Failed Login (Invalid Credentials)", () => {
  it("should reject authentication and not issue any token", async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/api/login", // auth-service port
        {
          username: "user1",
          password: "wrongpassword"
        }
      );

      // If request succeeds, this is a FAIL
      throw new Error("Authentication should have failed but succeeded");

    } catch (error) {
      // Axios throws for non-2xx responses
      const response = error.response;

      // HTTP failure expected
      expect(response.status).toBe(401); // or 400 depending on backend design

      // No token should be issued
      expect(response.data.access_token).toBeUndefined();

      // Error message should be present
      expect(response.data).toBeDefined();
      expect(response.data.message || response.data.error).toBeDefined();
    }
  });
});
