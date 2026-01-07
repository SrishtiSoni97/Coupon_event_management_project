function goUser() {
  window.location.href = "/user-dashboard/";
}

function addToCart(title, price) {
  const cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.push({title, price});
  localStorage.setItem("cart", JSON.stringify(cart));
  alert("Added to cart");
}
