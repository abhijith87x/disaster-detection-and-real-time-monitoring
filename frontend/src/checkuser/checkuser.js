export async function checkuser() {
    return  fetch("http://localhost:8000/profile",{
      method : 'GET',
      credentials: 'include'
  });
}