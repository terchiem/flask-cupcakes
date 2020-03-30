function handleSubmitBtn(evt){
  return true
}

async function start(){
  console.log("we're here")
  $('#submit_btn').on("click",handleSubmitBtn)

  let response = await axios.get('/api/cupcakes')
  let cupcakes = response.data.cupcakes
 

  let list = $('ul')
  
  console.log(cupcakes)

  for (let i=0; i < cupcakes.length; i++ ){
    list.append(`<li>
      <img src="${cupcakes[i].image}"> 
      ${cupcakes[i].flavor}
      ${cupcakes[i].size}
      rating: ${cupcakes[i].rating}
      </li>`
    )
  }
  
}


$(document).ready(start);
