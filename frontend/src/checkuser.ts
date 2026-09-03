export  function checkuser():Promise<Response>{
    return  fetch("/api/oauth/profile",{
      method : 'GET',
      credentials: 'include'
  });
}