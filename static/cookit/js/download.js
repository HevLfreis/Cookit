/**
 * Created by hevlhayt@foxmail.com
 * Date: 2016/7/2
 * Time: 19:08
 */

$('.domain').change(function(){

    var $form = $(this).parents(".form-group"),
          $topic = $form.next().find('.topic'),
          $submit_text = $form.next().next().find('textarea');

    $topic.hide();

    var domain = $(this).val();
    $topic.siblings('#'+$(this).val()).show().children().dblclick(function(){
    $submit_text.val($submit_text.val()+domain+'.'+$(this).val()+';');
});
}).children().dblclick(function(){

    var $form = $(this).parents(".form-group"),
          $topic = $form.next().find('.topic'),
          $submit_text = $form.next().next().find('textarea');
    console.log($submit_text);

    var domain = $(this).val();

    $.each($topic.find('#form-'+domain).children(), function(){
        $submit_text.val($submit_text.val()+domain+'.'+$(this).val()+';');
    });
});


$('.download').click(function(){
    var $dl_btn = $(this),
        $submit_text = $(this).siblings('fieldset').find('textarea');
    if(!$submit_text.val()) {
      alert('Please select at least one topic ! ');
      return
    }

    $dl_btn.addClass('disabled');
    $('textarea').attr('disabled', true);
    $('body').addClass('waiting');

    $.ajax({
        url: '/data/',
        timeout: 50000,
        type: 'post',
        data: {topics: $submit_text.val(), t: $dl_btn.attr('id')},
        success: function (result) {
        $dl_btn.removeClass('disabled');
        $('textarea').attr('disabled', false);
        $('body').removeClass('waiting');

        var filename = result.filename;
        console.log($dl_btn.parents().find('#form-last:first'));
        $dl_btn.parent().after(result.html);

        window.location.href='/static/temp/'+filename+'.zip';
        $submit_text.val('');

        },
        error: function() {
            $dl_btn.removeClass('disabled');
            $('textarea').attr('disabled', false);
            $('body').removeClass('waiting');
        }
    });
});

fd.jQuery();

function fileProcess(e, files) {
    var $submit_text = $(this).find('textarea');
    $.each(files, function (i, file) {

        var str = '';
        var reader = new FileReader();

        reader.onload = function(e){
            var data = e.target.result;
            try {
              var workbook = XLSX.read(data, {type: 'binary'});
            }
            catch(err) {
                alert("Not supported file: "+file.name);
                return;
            }

            var worksheet = workbook.Sheets[workbook.SheetNames[1]];
            for (z in worksheet) {

                if(z[0] === '!'|| z === 'C1' || z[0] !== 'C') continue;
                str += worksheet[z].v + ';'
            }
            $submit_text.val($submit_text.val()+str);
        };
        reader.readAsBinaryString(file.nativeFile);
    })
}

$('#cop-file-zone')
    .filedrop({'input':false})
    .on('fdsend', fileProcess);
$('#hrl-file-zone')
    .filedrop({'input':false})
    .on('fdsend', fileProcess);
$('#pat-file-zone')
    .filedrop({'input':false})
    .on('fdsend', fileProcess);





//var czone = new FileDrop('cop-file-zone', {'input':false}),
//    hzone = new FileDrop('hrl-file-zone', {'input':false}),
//    pzone = new FileDrop('pat-file-zone', {'input':false});
//
//
//function fileDrop(files) {
//
//    var $submit_text = $(fd.byID('submit-text'));
//
//    files.each()
//}
//
//czone.event('send', fileDrop);
//hzone.event('send', fileDrop);
//pzone.event('send', fileDrop);