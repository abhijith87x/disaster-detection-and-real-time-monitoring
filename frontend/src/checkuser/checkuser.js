export async function checkuser() {
    return  fetch("/profile",{
      method : 'GET',
      credentials: 'include'
  });
}