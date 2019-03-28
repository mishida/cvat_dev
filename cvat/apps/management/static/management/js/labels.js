$(function () {
    // formのidカウント
    var frm_cnt = 0;

    // 一つ上のformをclone
    $(document).on('click', 'span.add', function () {
        var original = $('#attr_spec\\[' + frm_cnt + '\\]');
        var originCnt = frm_cnt;

        //  オリジナルのラジオボタンの値を記憶(formを追加すると初期化される為)
        var originPrefix = $("input[name='prefix\\[" + frm_cnt + "\\]']:checked").val();
        var originInType = $("input[name='input_type\\[" + frm_cnt + "\\]']:checked").val();

        frm_cnt++;

        // formをclone
        original
            .clone()
            .hide()
            .insertAfter(original)
            .attr('id', 'attr_spec[' + frm_cnt + ']')
            .find("input[type='radio'][checked]").prop('checked', true)
            .end()
            .find('input, textarea').each(function (idx, obj) {
                $(obj).attr({
                    id: $(obj).attr('id').replace(/\[[0-9]\]+$/, '[' + frm_cnt + ']'),
                    name: $(obj).attr('name').replace(/\[[0-9]\]+$/, '[' + frm_cnt + ']')
                });
                $(obj).val('');
            });

        // clone取得
        var clone = $('#attr_spec\\[' + frm_cnt + '\\]');
        clone.children('span.close').show();
        clone.slideDown('slow');

        // originalラジオボタン復元
        original.find("input[name='prefix\\[" + originCnt + "\\]'][value='" + originPrefix + "']").prop('checked', true);
        original.find("input[name='input_type\\[" + originCnt + "\\]'][value='" + originInType + "']").prop('checked', true);
    });

    // close object
    $(document).on('click', 'span.close', function () {
        var removeObj = $(this).parent();
        removeObj.fadeOut('fast', function () {
            removeObj.remove();

            // 番号振り直し
            frm_cnt = 0;
            $(".attr-spec[id^='form_block']").each(function (index, formObj) {
                if ($(formObj).attr('id') != 'attr_spec[0]') {
                    frm_cnt++;
                    $(formObj)
                        .attr('id', 'attr_spec[' + frm_cnt + ']') // id属性を変更。
                        .find('input, textarea').each(function (idx, obj) {
                            $(obj).attr({
                                id: $(obj).attr('id').replace(/\[[0-9]\]+$/, '[' + frm_cnt + ']'),
                                name: $(obj).attr('name').replace(/\[[0-9]\]+$/, '[' + frm_cnt + ']')
                            });
                        });
                }
            });
        });
    });
});