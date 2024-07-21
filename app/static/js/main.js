// 通用函数：打开模态框
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// 通用函数：关闭模态框
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 通用函数：发送POST请求
async function postData(url, data) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

// 通用函数：发送GET请求
async function getData(url) {
    const response = await fetch(url);
    return response.json();
}

// 通用函数：刷新表格数据
function refreshTable(tableId, data, columns) {
    const table = document.getElementById(tableId);
    const tbody = table.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = tbody.insertRow();
        columns.forEach(column => {
            const cell = row.insertCell();
            cell.textContent = item[column];
        });
    });
}

// 页面加载完成后执行的函数
document.addEventListener('DOMContentLoaded', function() {
    // 这里可以添加页面初始化的代码
    console.log('页面加载完成');
});

// 示例：添加商品的函数
async function addProduct(event) {
    event.preventDefault();
    const form = event.target;
    const data = {
        name: form.name.value,
        category_id: form.category_id.value,
        price: form.price.value,
        stock: form.stock.value,
        supplier_id: form.supplier_id.value
    };

    try {
        const result = await postData('/product/add', data);
        if (result.success) {
            alert('商品添加成功');
            closeModal('addProductModal');
            // 刷新商品列表
        } else {
            alert('商品添加失败');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('发生错误，请稍后再试');
    }
}

// 其他模块的函数可以按照类似的方式实现}