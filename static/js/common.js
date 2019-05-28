function Common() {
  $("input[type='file']").change(function(e){
    const file_name = e.target.files[0].name;
    $(this).next('.custom-file-label').html(file_name);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  Common()
});