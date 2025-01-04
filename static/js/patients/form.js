document.addEventListener('DOMContentLoaded', function() {
    // Funciones auxiliares
    function createFormGroup(label, input) {
        const group = document.createElement('div');
        group.className = 'form-group';
        
        const labelElement = document.createElement('label');
        labelElement.textContent = label;
        
        group.appendChild(labelElement);
        group.appendChild(input);
        
        return group;
    }

    function createInput(type, name, placeholder = '', value = '', required = false) {
        const input = document.createElement('input');
        input.type = type;
        input.name = name;
        input.className = 'form-input';
        input.placeholder = placeholder;
        input.value = value;
        input.required = required;
        return input;
    }

    function createRemoveButton() {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'btn btn-icon btn-remove';
        button.onclick = function() {
            this.closest('.formset-item').remove();
        };
        button.innerHTML = '<span>×</span>';
        return button;
    }

    // Inicializar contadores
    let parentIndex = 0;
    let siblingIndex = 0;
    let householdIndex = 0;

    // Cargar datos existentes si están disponibles
    const existingDataElement = document.getElementById('existingData');
    if (existingDataElement) {
        const existingData = JSON.parse(existingDataElement.textContent);
        
        // Cargar padres existentes
        if (existingData.parents) {
            existingData.parents.forEach(parent => {
                window.addParent(parent);
            });
        }
        
        // Cargar hermanos existentes
        if (existingData.siblings) {
            existingData.siblings.forEach(sibling => {
                window.addSibling(sibling);
            });
        }
        
        // Cargar habitantes del hogar existentes
        if (existingData.household_members) {
            existingData.household_members.forEach(member => {
                window.addHouseholdMember(member);
            });
        }

        // Marcar opciones del historial médico
        if (existingData.medical_history) {
            Object.entries(existingData.medical_history).forEach(([key, value]) => {
                const radio = document.querySelector(`input[name="medical_${key}"][value="${value}"]`);
                if (radio) {
                    radio.checked = true;
                }
            });
        }
    }

    // Manejadores para los botones de agregar
    document.getElementById('addParentBtn')?.addEventListener('click', () => window.addParent());
    document.getElementById('addSiblingBtn')?.addEventListener('click', () => window.addSibling());
    document.getElementById('addHouseholdMemberBtn')?.addEventListener('click', () => window.addHouseholdMember());

    // Previsualización de la foto
    const photoInput = document.querySelector('input[type="file"]');
    const photoPreview = document.getElementById('photoPreview');

    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.innerHTML = `<img src="${e.target.result}" alt="Vista previa">`;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

        // Función para agregar padre
    // Función para agregar padre
window.addParent = function(data = null) {
    const container = document.getElementById('parentsFormset');
    const formDiv = document.createElement('div');
    formDiv.className = 'formset-item';
    
    const formGrid = document.createElement('div');
    formGrid.className = 'form-grid';
    
    // Campos del formulario con nombres corregidos
    formGrid.appendChild(createFormGroup('Nombre', 
        createInput('text', `parent_name[]`, 'Nombre completo', data?.name || '', true)));
    formGrid.appendChild(createFormGroup('Fecha de nacimiento', 
        createInput('date', `parent_birth_date[]`, '', data?.birth_date?.split('T')[0] || '', true)));
    formGrid.appendChild(createFormGroup('Escolaridad', 
        createInput('text', `parent_education_level[]`, 'Nivel de estudios', data?.education_level || '')));
    formGrid.appendChild(createFormGroup('Ocupación', 
        createInput('text', `parent_occupation[]`, 'Ocupación actual', data?.occupation || '')));
    
    const historyTextarea = document.createElement('textarea');
    historyTextarea.name = `parent_pathological_history[]`;
    historyTextarea.className = 'form-input';
    historyTextarea.placeholder = 'Antecedentes patológicos';
    historyTextarea.rows = 3;
    if (data?.pathological_history) {
        historyTextarea.value = data.pathological_history;
    }
    
    const historyGroup = createFormGroup('Antecedentes patológicos', historyTextarea);
    historyGroup.className = 'form-group full-width';
    formGrid.appendChild(historyGroup);
    
    formDiv.appendChild(formGrid);
    formDiv.appendChild(createRemoveButton());
    container.appendChild(formDiv);
    
    parentIndex++;
};

// Función para agregar hermano
window.addSibling = function(data = null) {
    const container = document.getElementById('siblingsFormset');
    const formDiv = document.createElement('div');
    formDiv.className = 'formset-item';
    
    const formGrid = document.createElement('div');
    formGrid.className = 'form-grid';
    
    // Campos del formulario con nombres corregidos
    formGrid.appendChild(createFormGroup('Nombre', 
        createInput('text', `sibling_name[]`, 'Nombre completo', data?.name || '', true)));
    formGrid.appendChild(createFormGroup('Fecha de nacimiento', 
        createInput('date', `sibling_birth_date[]`, '', data?.birth_date?.split('T')[0] || '', true)));
    formGrid.appendChild(createFormGroup('Escolaridad', 
        createInput('text', `sibling_education_level[]`, 'Nivel de estudios', data?.education_level || '')));
    
    const addictionsGroup = document.createElement('div');
    addictionsGroup.className = 'form-group';
    const addictionsLabel = document.createElement('label');
    addictionsLabel.textContent = '¿Tiene adicciones?';
    const addictionsCheckbox = createInput('checkbox', `sibling_has_addictions[]`, '');
    if (data?.has_addictions) {
        addictionsCheckbox.checked = true;
    }
    addictionsGroup.appendChild(addictionsLabel);
    addictionsGroup.appendChild(addictionsCheckbox);
    formGrid.appendChild(addictionsGroup);
    
    const historyTextarea = document.createElement('textarea');
    historyTextarea.name = `sibling_pathological_history[]`;
    historyTextarea.className = 'form-input';
    historyTextarea.placeholder = 'Antecedentes patológicos';
    historyTextarea.rows = 3;
    if (data?.pathological_history) {
        historyTextarea.value = data.pathological_history;
    }
    
    const historyGroup = createFormGroup('Antecedentes patológicos', historyTextarea);
    historyGroup.className = 'form-group full-width';
    formGrid.appendChild(historyGroup);
    
    formDiv.appendChild(formGrid);
    formDiv.appendChild(createRemoveButton());
    container.appendChild(formDiv);
    
    siblingIndex++;
};

// Función para agregar habitante del hogar
window.addHouseholdMember = function(data = null) {
    const container = document.getElementById('householdFormset');
    const formDiv = document.createElement('div');
    formDiv.className = 'formset-item';
    
    const formGrid = document.createElement('div');
    formGrid.className = 'form-grid';
    
    // Campos del formulario con nombres corregidos
    formGrid.appendChild(createFormGroup('Nombre', 
        createInput('text', `household_name[]`, 'Nombre completo', data?.name || '', true)));
    formGrid.appendChild(createFormGroup('Relación', 
        createInput('text', `household_relationship[]`, 'Parentesco o relación', data?.relationship || '', true)));
    
    const historyTextarea = document.createElement('textarea');
    historyTextarea.name = `household_medical_history[]`;
    historyTextarea.className = 'form-input';
    historyTextarea.placeholder = 'Antecedentes médicos';
    historyTextarea.rows = 3;
    if (data?.medical_history) {
        historyTextarea.value = data.medical_history;
    }
    
    const historyGroup = createFormGroup('Antecedentes médicos', historyTextarea);
    historyGroup.className = 'form-group full-width';
    formGrid.appendChild(historyGroup);
    
    formDiv.appendChild(formGrid);
    formDiv.appendChild(createRemoveButton());
    container.appendChild(formDiv);
    
    householdIndex++;
};

    // Configurar botones de agregar
    document.getElementById('addParentBtn').addEventListener('click', () => addParent());
    document.getElementById('addSiblingBtn').addEventListener('click', () => addSibling());
    document.getElementById('addHouseholdMemberBtn').addEventListener('click', () => addHouseholdMember());



    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    photoPreview.innerHTML = `<img src="${e.target.result}" alt="Vista previa">`;
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

});

