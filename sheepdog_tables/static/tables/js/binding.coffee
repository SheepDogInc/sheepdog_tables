$(document).ready ->

  _deParamd = $.deparam.querystring true

  # Paginator
  ($ ".pagination a.table-pager").on "click", (ev) ->
    $el = $ ev.currentTarget
    urlNamespace = $el.data 'ns'
    _deParamd[urlNamespace + '-page'] = $el.data 'page'
    document.location.search = "?" + ($.param _deParamd, true)
    false

  # Inline Sorter
  ($ "a.table-sorter").on "click", (ev) ->
    $el = $ ev.currentTarget
    urlNamespace = $el.data 'ns'
    _deParamd[urlNamespace + '-sort'] = $el.data 'sort'
    document.location.search = "?" + ($.param _deParamd, true)
    false

  # EditTables
  ($ "[data-edittable-form]").each ->
    $btn = $ this
    data = $btn.data()
    $btn.on "click", ->
      ($ "##{data.edittableForm}").submit()

  ($ ".table-form input").on "change", ->
    $input = $ this
    $input.addClass "changed"
  @
