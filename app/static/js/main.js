function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

async function postData(url, data) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };

        // 尝试获取 CSRF 令牌，如果存在就添加到 headers 中
        const csrfToken = document.querySelector('meta[name="csrf-token"]');
        if (csrfToken) {
            headers['X-CSRFToken'] = csrfToken.getAttribute('content');
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error("Fetch error:", error);
        throw error;
    }
}

async function getData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error("Fetch error:", error);
        throw error;
    }
}

function refreshTable(tableId, data, columns) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = '';
    data.forEach(item => {
        const tr = document.createElement('tr');
        columns.forEach(column => {
            const td = document.createElement('td');
            td.textContent = item[column];
            tr.appendChild(td);
        });
        const actionTd = document.createElement('td');
        actionTd.innerHTML = `
            <button class="editProductBtn" data-id="${item.id}">修改</button>
            <button class="deleteProductBtn" data-id="${item.id}">删除</button>
        `;
        tr.appendChild(actionTd);
        tbody.appendChild(tr);
    });
}

async function addProduct(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    try {
        const result = await postData(form.action, Object.fromEntries(formData));
        if (result.success) {
            alert('商品添加成功');
            closeModal('addProductModal');
            location.reload();
        } else {
            alert('商品添加失败: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('发生错误，请稍后再试');
    }
}

async function editProduct(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const productId = formData.get('id');
    try {
        console.log('Editing product:', productId);
        const result = await postData(`/product/edit/${productId}`, Object.fromEntries(formData));
        console.log('Edit result:', result);
        if (result.success) {
            alert('商品修改成功');
            closeModal('editProductModal');
            location.reload();
        } else {
            alert('商品修改失败: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('发生错误，请稍后再试');
    }
}

async function deleteProduct(productId) {
    if (confirm('确定要删除这个商品吗？')) {
        try {
            const result = await postData(`/product/delete/${productId}`, {});
            if (result.success) {
                alert('删除商品成功');
                location.reload();
            } else {
                alert('删除商品失败: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('发生错误，请稍后再试');
        }
    }
}

async function searchProducts(query) {
    try {
        const products = await getData(`/product/search?query=${query}`);
        refreshTable('productTable', products, ['id', 'name', 'category', 'price', 'stock', 'supplier']);
    } catch (error) {
        console.error('Error:', error);
        alert('搜索出错，请稍后再试');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成');

    const addProductBtn = document.getElementById('addProductBtn');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', () => openModal('addProductModal'));
    }

    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', addProduct);
    }

    const editProductForm = document.getElementById('editProductForm');
    if (editProductForm) {
        editProductForm.addEventListener('submit', editProduct);
    }

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('editProductBtn')) {
            const productId = event.target.getAttribute('data-id');
            getData(`/product/${productId}`).then(product => {
                document.getElementById('editProductId').value = product.product_id;
                document.getElementById('editName').value = product.name;
                document.getElementById('editCategory').value = product.category_id;
                document.getElementById('editPrice').value = product.price;
                document.getElementById('editStock').value = product.stock;
                document.getElementById('editSupplier').value = product.supplier_id;
                openModal('editProductModal');
            }).catch(error => {
                console.error('Error fetching product data:', error);
                alert('获取商品信息失败，请稍后再试');
            });
        }

        if (event.target.classList.contains('deleteProductBtn')) {
            const productId = event.target.getAttribute('data-id');
            deleteProduct(productId);
        }
    });

    const searchProductInput = document.getElementById('searchProduct');
    if (searchProductInput) {
        searchProductInput.addEventListener('input', function() {
            searchProducts(this.value);
        });
    }

    document.querySelectorAll('.closeModal').forEach(btn => {
        btn.addEventListener('click', function() {
            closeModal(this.closest('.modal').id);
        });
    });
});