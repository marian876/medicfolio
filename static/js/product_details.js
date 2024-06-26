document.addEventListener('DOMContentLoaded', function() {
    const selectProducto = document.getElementById('id_producto');
    const precioInput = document.getElementById('id_precio_compra');

    if (selectProducto && precioInput) { // Asegura que ambos elementos existen
        selectProducto.addEventListener('change', function() {
            const productId = this.value;
            fetch(`/stock/producto_detalle/?id=${productId}`)
                .then(response => response.json())
                .then(data => {
                    precioInput.value = data.precio;  
                })
                .catch(error => console.error('Error:', error));
        });
    } else {
        console.error('Elementos del DOM no encontrados');
    }
});
