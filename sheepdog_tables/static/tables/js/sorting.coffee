($ document).ready ->
  _deParamd = $.deparam.querystring true
  ($ "a.table-sorter").on "click", (ev) ->
    $el = $ ev.currentTarget
    urlNamespace = $el.data 'ns'
    _deParamd[urlNamespace + '-sort'] = $el.data 'sort'
    document.location.search = "?" + ($.param _deParamd, true)
    false
  @
