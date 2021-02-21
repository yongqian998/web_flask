$(function () {
    $("#btn-email").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        if(!email){
            zlalert.alertInfoToast('请输入邮箱');
            return;
        }
        zlajax.get({
            'url': '/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('邮件发送成功！请注意查收！');
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});
