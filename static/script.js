"use strict";

const $list = $("#cupcakeList");
const $form = $("form");
const $flavor = $("#flavor");
const $size = $("#size");
const $rating = $("#rating");
const $imageUrl = $("#imageUrl");

async function start() {
  $list.empty();
  let response = await axios.get("/api/cupcakes");
  console.log(response.data.cupcakes);

  createList(response.data.cupcakes)
}

async function createList(cupcakesArr) {
  for (let i = 0; i < cupcakesArr.length; i++) {
    const $listItem = $("<li>");

    let flavor = cupcakesArr[i].flavor;
    let image_url = cupcakesArr[i].image;
    let rating = cupcakesArr[i].rating;
    let size = cupcakesArr[i].size;

    let $description = $(`<p>Flavor: ${flavor}, Rating: ${rating}, Size: ${size}</p>`);
    let $image = $(`<img src=${image_url}></img>`);

    $listItem.append($description);
    $listItem.append($image);

    $list.append($listItem);
  }

}

$form.submit(axiosPost);

async function axiosPost(evt) {
  evt.preventDefault();
  console.log("WORKS");
  console.log($flavor.val());
  console.log($imageUrl.val());

  let data = {
    "flavor": $flavor.val(),
    "size": $size.val(),
    "rating": $rating.val(),
    "image": $imageUrl.val()
  }

  let response = await axios.post(
    "/api/cupcakes", data);

  console.log(response.data);
  $form.trigger("reset");

  start();


}


start();