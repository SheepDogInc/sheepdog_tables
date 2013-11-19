($ document).ready ->
  _deParamd = $.deparam.querystring true
  ($ ".pagination a.table-pager").on "click", (ev) ->
    $el = $ ev.currentTarget
    urlNamespace = $el.data 'ns'
    _deParamd[urlNamespace + '-page'] = $el.data 'page'
    document.location.search = "?" + ($.param _deParamd, true)
    false
  @
