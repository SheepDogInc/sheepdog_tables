cleanse = (value) -> if value? and value[0] is '-' then value.substring(1, value.length) else value
gettext = (str) -> str

class SortOptionCollection extends Backbone.Collection
  findByValue: (value) ->
    @filter (model) ->
      model.get('value') is value

class SortByView extends Backbone.View
  initialize: ->
    @$el.val @options.initialValue
    @model.on "change:order", @update
    @$el.on "change", @selectChange

  render: ->
    @$el.select2
      width: '100%'
    @update()
    @$el.select2 "val", @$el.val()
    @

  selectChange: =>
    @model.set 'selected', cleanse @$el.val()

  update: =>
    for opt in @$el.find 'option'
      $opt = $ opt
      value = cleanse $opt.val()
      $opt.val if @model.get 'order' then "-#{value}" else value


class SortOrderView extends Backbone.View
  text_pairs:
    alpha: [gettext('A to Z'), gettext('Z to A')]
    num: [gettext('1 to 9'), gettext('9 to 1')]
    date: [gettext('Oldest to Newest'), gettext('Newest to Oldest')]

  initialize: ->
    @model.on "change:selected", @update
    @$el.on "change", @selectChange

  render: ->
    @$el.select2
      width: '100%'
    @update()
    @

  selectChange: =>
    @model.set 'order', parseInt @$el.val()

  update: =>
    sel = @model.get 'selected'
    m = _.first @collection.findByValue(@model.get 'selected')
    for opt in @$el.find "option"
      $opt = $ opt
      $opt.text @text_pairs[m.get 'order'][$opt.val()]
    @$el.select2 "val", "#{@model.get 'order'}"


class @SortController
  queryDict: (key) ->
    _deParamd = $.deparam.querystring()
    if key of _deParamd then _deParamd[key] else false

  constructor: (sortData) ->
    return @ if not sortData?
    defaultDir = if cleanse sortData.default is sortData.default then 0 else 1

    selected = cleanse @queryDict('srtby') or sortData.default
    optionsCollection = new SortOptionCollection

    optionsModel = new Backbone.Model
      order: parseInt @queryDict('srton') or defaultDir
      selected: selected

    for key, value of sortData.pairs
      optionsCollection.add(new Backbone.Model
        value: key
        order: value)

    sortBy = new SortByView
      el: "select#id_srtby"
      model: optionsModel
      collection: optionsCollection
      initialValue: @queryDict('srtby') or sortData.default

    sortOrder = new SortOrderView
      el: "select#id_srton"
      model: optionsModel
      collection: optionsCollection

    sortBy.render()
    sortOrder.render()
