$(document).ready(function () {
    show_ranking();
});

// 랭킹 보여주는 함수
function show_ranking() {
    $.ajax({
        type: 'GET',
        url: '/api/result',
        data: {},
        success: function (response) {
            let rows = response['ranking']
            rows.sort(function (a,b){
                return b.score - a.score
            });
            console.log(rows)
            let ranking = 0;
            for (let i = 0; i < 3; i++) {
                let id = rows[i]['id'];
                let score = rows[i]['score'];
                ranking = ranking+1;
                let temp_html = `<tr>
                                    <th scope="row">${ranking}등</th>
                                    <td>${id}</td>
                                    <td>${score}점</td>

                                </tr>`
                $('#rank').append(temp_html)
            }

        }

    });
}