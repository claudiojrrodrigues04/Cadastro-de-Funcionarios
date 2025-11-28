// app/static/app.js

document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA PARA FORMULÁRIOS (POST / PUT) ---
    // Encontra todos os formulários que têm o 'data-method'
    const forms = document.querySelectorAll('form[data-method]');
    
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Impede o envio normal
            
            const action = form.action;
            const method = form.getAttribute('data-method').toUpperCase();
            
            // Se for POST, deixa o navegador tratar (embora possamos usar fetch)
            if (method === 'POST') {
                form.submit();
                return;
            }

            // Se for PUT (para Edição)
            if (method === 'PUT') {
                const formData = new FormData(form);
                
                // FastAPI espera os dados do Form() como 'x-www-form-urlencoded'
                const body = new URLSearchParams(formData); 
                
                fetch(action, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: body
                })
                .then(response => {
                    if (response.ok) {
                        // O 'employees.py' retorna 204
                        // Redireciona para a lista após sucesso
                        window.location.href = '/employees'; 
                    } else {
                        alert('Erro ao atualizar. Verifique os dados.');
                    }
                })
                .catch(err => {
                    console.error('Erro no fetch PUT:', err);
                    alert('Erro de rede ao atualizar.');
                });
            }
        });
    });

    // --- LÓGICA PARA BOTÕES DE DELEÇÃO (DELETE) ---
    // (Isto assume que na sua lista (index.html)
    // os botões de apagar têm a classe 'delete-btn' e 'data-id')
    
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            
            if (!confirm('Tem a certeza que quer apagar este funcionário?')) {
                return;
            }
            
            const id = button.getAttribute('data-id');
            
            fetch(`/employees/${id}`, { method: 'DELETE' })
            .then(response => {
                if(response.ok) {
                    // O 'employees.py' retorna 204
                    // Recarrega a página para mostrar a lista atualizada
                    window.location.reload(); 
                } else {
                    alert('Erro ao apagar o funcionário.');
                }
            })
            .catch(err => {
                console.error('Erro no fetch DELETE:', err);
                alert('Erro de rede ao apagar.');
            });
        });
    });

});

// Espera o documento HTML estar 100% carregado
document.addEventListener("DOMContentLoaded", () => {
    
    // 1. Encontra TODOS os botões de excluir
    const deleteButtons = document.querySelectorAll(".delete-employee-btn");

    // 2. Adiciona um "ouvinte" de clique em cada um
    deleteButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            
            // 3. Pede confirmação
            const confirmed = confirm("Tem certeza que deseja excluir este funcionário? Esta ação não pode ser desfeita.");
            
            if (confirmed) {
                // 4. Pega o ID guardado no botão (data-id)
                const employeeId = event.target.dataset.id;
                
                // 5. Envia a requisição DELETE para a API
                fetch(`/employees/${employeeId}`, {
                    method: "DELETE",
                })
                .then(response => {
                    // A rota de delete retorna 204 (No Content)
                    if (response.status === 204) {
                        // 6. Sucesso! Remove a linha da tabela
                        document.getElementById(`employee-row-${employeeId}`).remove();
                    } else {
                        // 7. Falha
                        alert("Não foi possível excluir o funcionário.");
                    }
                })
                .catch(error => {
                    console.error("Erro ao excluir:", error);
                    alert("Ocorreu um erro de rede.");
                });
            }
        });
    });

});

const deleteDeptButtons = document.querySelectorAll(".delete-department-btn");

    deleteDeptButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            
            if (confirm("Tem certeza que deseja excluir este departamento?")) {
                const id = event.target.dataset.id;
                
                // Muda a URL para /departments/ID
                fetch(`/departments/${id}`, {
                    method: "DELETE",
                })
                .then(response => {
                    if (response.status === 204) {
                        // Remove a linha da tabela (department-row-ID)
                        const row = document.getElementById(`department-row-${id}`);
                        if (row) row.remove();
                    } else {
                        alert("Não foi possível excluir (Verifique se há funcionários neste departamento).");
                    }
                })
                .catch(error => {
                    console.error("Erro:", error);
                });
            }
        });
    });

const deletePosButtons = document.querySelectorAll(".delete-position-btn");

    deletePosButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            
            if (confirm("Tem certeza que deseja excluir este cargo?")) {
                const id = event.target.dataset.id;
                
                // Muda a URL para /positions/ID
                fetch(`/positions/${id}`, {
                    method: "DELETE",
                })
                .then(response => {
                    if (response.status === 204) {
                        // Remove a linha da tabela (position-row-ID)
                        const row = document.getElementById(`position-row-${id}`);
                        if (row) row.remove();
                    } else {
                        alert("Não foi possível excluir (Verifique se há funcionários neste cargo).");
                    }
                })
                .catch(error => {
                    console.error("Erro:", error);
                });
            }
        });
    });

