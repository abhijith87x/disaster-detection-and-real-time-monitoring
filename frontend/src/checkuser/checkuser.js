export async function checkuser() {
    return  await fetch("/profile",{
      method : 'GET',
      credentials: 'include'
  });
}