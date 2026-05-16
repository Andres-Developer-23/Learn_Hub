var qCount = {% if exam %}{{ exam.questions.all|length }}{% else %}0{% endif %};
function addQuestion() {
    var container = document.getElementById('questions-container');
    var idx = qCount++;
    var div = document.createElement('div');
    div.className = 'qbox';
    div.setAttribute('data-q', idx);
    var opts = '';
    for (var o = 0; o < 4; o++) {
        opts += '<div class="opt-row"><span class="opt-label">' + (o+1) + '.</span><input type="text" name="option_' + idx + '_' + o + '" placeholder="Opción ' + (o+1) + '"><input type="radio" name="correct_' + idx + '" value="' + o + '"></div>';
    }
    div.innerHTML = '<h4>Pregunta ' + (idx+1) + '</h4><div class="mf"><textarea name="question_text[]" rows="2" required></textarea></div><div style="font-size:.72rem;color:var(--mu);margin-bottom:.4rem">Opciones (marca la correcta):</div>' + opts + '<button type="button" class="btn btn-sm btn-err" onclick="this.closest(\'.qbox\').remove()" style="margin-top:.5rem;font-size:.7rem;padding:.25rem .6rem">🗑️ Quitar</button>';
    container.appendChild(div);
}