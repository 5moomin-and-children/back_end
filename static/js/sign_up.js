//비밀번호 확인 스크립트
function check_pw() {
  var p1 = document.getElementById('password1').value;
  var p2 = document.getElementById('password2').value;
  if(p1 != p2) {
    document.getElementById('check').innerHTML = 'X'
    document.getElementById('check').style.color = 'red'
    document.getElementById('check').style.fontSize = "10vw"
  }
  else {
    document.getElementById('check').innerHTML = 'O'
    document.getElementById('check').style.color = 'green'
    document.getElementById('check').style.fontSize = "10vw"
  }
}

function register() {
    $.ajax({
        type: "POST",
        url: "/api/sign_up",
        data: {
            id: $('#userid').val(),
            pw: $('#password2').val()
        },
        success: function (response) {
            if (response['result'] == 'success') {
                alert('회원가입이 완료되었습니다.')
                window.location.href = '/'
            } else {
                alert(response['msg'])
            }
        }
    })
}

function confirmEmail() {
        $.ajax({
            type: "POST",
            url: "/api/check_id",
            data: {
                id: $('#userid').val(),
            },
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg'])
            } else {
                alert(response['msg'])
            }
        }
    })
}
