function tablePageSubmit(e){
    var keycode = event.keycode;            
    if(event.keyCode == 13){
        var str = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/'));
        var pageURL = str+"/" + $(e).val()+"?count="+$('.list-table-info .table-count button').text().trim();
        
        document.location.href=pageURL;
    }            
}
function tablePageChange(param){
    var str = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/'));
    var pageURL = str+"/" + param+"?count="+$('.list-table-info .table-count button').text().trim();
    
    document.location.href=pageURL;
}
function tableCountChange(count){
    var str = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/'));
    document.location.href=str+"/"+"?count="+$(count).text().trim();
}