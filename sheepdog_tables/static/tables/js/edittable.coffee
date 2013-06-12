$(document).ready ->
  ($ "[data-edittable-form]").each ->
    $btn = $ this
    data = $btn.data()
    $btn.on "click", ->
      ($ "##{data.edittableForm}").submit()

  ($ ".table-form input").on "change", ->
    $input = $ this
    $input.addClass "changed"

