function upload(file) {
    var xhr = new XMLHttpRequest();
    xhr.open('post','/app/upload',true);
    xhr.onload=function () {
        if(xhr.status==200&&xhr.readyState==4){
            data = JSON.parse(xhr.responseText);
            if (data.state=='ok'){
                $('#userImg').attr('src','/static/'+data.path)
            }
        }

    };
    var formdata = new FormData();
    formdata.append('img',file);
    xhr.send(formdata);
    
}