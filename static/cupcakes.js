async function handleSubmitBtn(evt){
  evt.preventDefault();

  let flavor = $('#flavor').val();
  let size = $('#size').val();
  let rating = $('#rating').val();
  let image = $('#image').val();

  let data = {
    flavor,
    size,
    rating,
    image
  }

  let response = await axios.post('/api/cupcakes', data);
  let cupcake = response.data.cupcake
  
  $('#cupcake-list').append(createCupcakeHTML(cupcake));
  $('form').trigger('reset');
}

/**
 * Search for a cupcake
 */
async function handleSearchBtn(evt) {
  evt.preventDefault();
  let flavor = $('#flavor').val();

  let response = await axios.get('/api/search', { params: {flavor}});
  let cupcakes = response.data.cupcakes

  let $cupcakeList = $('#cupcake-list');
  
  $cupcakeList.empty();
  for (let cupcake of cupcakes) {
    $cupcakeList.append(createCupcakeHTML(cupcake));
  }
  $('form').trigger('reset');
}

function createCupcakeHTML(cupcake) {
  return $(`<li>
    <img height="80" src="${cupcake.image}"> 
    ${cupcake.flavor}
    ${cupcake.size}
    rating: ${cupcake.rating}
  </li>`);
}

async function start(){
  $('#submit_btn').on("click",handleSubmitBtn)
  $('#search_btn').on("click", handleSearchBtn)

  let response = await axios.get('/api/cupcakes')
  let cupcakes = response.data.cupcakes
 
  let list = $('#cupcake-list');

  for (let i=0; i < cupcakes.length; i++ ){
    list.append(createCupcakeHTML(cupcakes[i]));
  }
}

$(start);
