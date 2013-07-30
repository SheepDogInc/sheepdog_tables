($ document).ready ->
  _deParamd = $.deparam.querystring true
  ($ ".pagination a.table-pager").on "click", (ev) ->
    $el = $ ev.target
    urlNamespace = $el.attr 'data-ns'
    _deParamd[urlNamespace + '-page'] = $el.attr 'data-page'
    document.location.search = "?" + ($.param _deParamd, true)
    false
  @