export function isAuthenticated() {
  return !!localStorage.getItem("token");
}

export function getAuthHeaders() {
  const token = localStorage.getItem("token");
  if (!token) return {};
  return {
    "Authorization": "Bearer " + token
  };
}
