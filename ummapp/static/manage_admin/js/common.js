function hideMsg(){
    $('#msg-info').css('display','none')
}

$('input[type=file]').on('change', prepareUpload);

function prepareUpload(event)
{
files = event.target.files;
}

var fileChange = function(){
  var files = $('input[name^="image_ref"]')[0].files
  if(files){
    for (var i=0;i<files.length;i++){
      filename = files[i].name;
      var allowedFiles = ["gif,jpg,jpeg,tiff,png,bmp"];
      if (!(/\.(gif|jpg|jpeg|tiff|png|bmp)$/i).test(filename)) {
        // inputted file path is not an image of one of the above types
        $('#span-msg').text('Please upload image only with extension ' + allowedFiles.join(', '))
        $('#msg-info').show();
        $('input[name^="image_ref"]').val('');
        $('.file-name').html('');
        return false;
      }
      hideMsg();
      $('.file-name').html(filename);
      return true;
    }
  }
}


