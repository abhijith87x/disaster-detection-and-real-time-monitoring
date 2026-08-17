export  function checkuser():Promise<Response>{
    return  fetch("/profile",{
      method : 'GET',
      credentials: 'include'
  });
}