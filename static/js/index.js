function addMembershipFunctionFields() {
    var numLabels = document.getElementById('num-labels').value;
    var container = document.getElementById('membership-functions-container');
    container.innerHTML = '';

    for (var i = 0; i < numLabels; i++) {
        var labelDiv = document.createElement('div');
        labelDiv.innerHTML = '<h4>Значение: </h4> <input type="text" id="input' + i + '" > ';

        var selectFuncType = document.createElement('select');
        selectFuncType.name = "Значение"+i
        selectFuncType.innerHTML = '<option value="1">Треугольная</option>'+
                                   '<option value="2">Трапециевидная</option>';

        (function(labelDiv) {
            selectFuncType.addEventListener('change', function() {
                var inputParams = labelDiv.querySelector('.input-params');
                inputParams.innerHTML = '';

                var numParams = parseInt(this.value) === 1 ? 3 : 4;

                for (var j = 0; j < numParams; j++) {
                    var inputParam = document.createElement('input');
                    inputParam.classList.add('input_value')
                    inputParam.type = 'number';
                    inputParam.step = 'any';
                    inputParam.name = 'input'+j;
                    inputParams.appendChild(inputParam);
                }
            });
        })(labelDiv);

        var inputParams = document.createElement('div');
        inputParams.classList.add('input-params');

        for (var j = 0; j < 3; j++) {
            var inputParam = document.createElement('input');
            inputParam.classList.add('input_value')
            inputParam.type = 'number';
            inputParam.step = 'any';
            inputParam.name = 'input'+j;
            inputParams.appendChild(inputParam);
        }

        labelDiv.appendChild(selectFuncType);
        labelDiv.appendChild(inputParams);
        container.appendChild(labelDiv);
    }
}
