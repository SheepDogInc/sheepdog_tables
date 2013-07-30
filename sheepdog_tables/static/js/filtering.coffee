# filtering.coffee
# Enhances the filter form on filterable reports to be more awesome.

# Filter Model
#
# The filter model stores a couple of useful parameters:
#  - text: shows up in the filter dropdown
#  - free: whether the filter is available to use
#  - id: selector for the original HTML element
#  - baseHtml: the inner HTML for the widget to render
#  - cleared: whether the model should forget about its value
class Filter extends Backbone.Model
  defaults:
    free: yes
    cleared: no

# A collection of Filter objects.
# This is will essentially be the core of the filtering controls functionality
# Most places are going to be listening to "changes" on the filters
# in order to act on changes in the 'free' state.
class FilterCollection extends Backbone.Collection
  model: Filter
  selectAvailable: (override) -> @filter (f) -> (f.get "free") isnt no

# And Individual widget that gets added and removed from the view
class FilterWidget extends Backbone.View
  className: "row-fluid"
  events:
    "click i.remove": "removeFilter"

  initialize: (options) ->
    {@model} = options
    @model.on "change:cleared", => @remove()
  clear: -> (@$ "input[type=text], select").val ""
  removeFilter: ->
    @remove()
    @model.set
      free: yes
      cleared: yes

  render: ->
    @$el.html """
      <div class="control-group">
        <i class="remove icon-remove"></i> #{ @model.get "baseHtml" }
      </div>
    """
    (@$ ".control-group").show()
    if @model.get "cleared"
      @clear()
    # Multi-selects become select2s
    (@$ ".selectmultiple").select2
      width: "100%"

    # Single selects become select2s
    (@$ "select").select2
      width: "100%"

    (@$ "select.rangechoice").select2
      width: "50%"

    # For two inputs (usually a date range), shrink up the size of boxes
    inputs = @$('input:not([id^="s2id_autogen"])')
    inputs.width "47.5%" if inputs.length is 2
    (@$ ".dateinput").datepicker format: "mm/dd/yyyy"
    @

# The dropdown box that says "Add Filter" and allows you to add
# new filters to the pool of in-use ones.
class FilterDropdown extends Backbone.View
  events:
    "click .dropdown-toggle, .dropdown-menu": "toggle"

  initialize: (options) ->
    {@root, @filters} = options
    $("html").on "mouseup", @document_mouseup
    @$el = @root
    @$el.addClass "dropdown"
    @filters.on "all", => @populate()
    @filters.on "addFilter", => @close()

  document_mouseup: (e) =>
    @$el.removeClass "open" if @$el.has(e.target).length == 0

  close: -> @$el.removeClass "open"
  toggle: ->
    @$el.toggleClass "open" unless @disabled
    false

  # refreshes the list of available filters and re-renders the
  # list.
  populate: ->
    filters = @filters.selectAvailable()
    ul = @$ ".dropdown-menu"
    if filters.length > 0
      @disabled = false
      (@$ "a").removeClass "disabled"
      ul.empty()
      for model in filters
        li = new FilterDropdownItem
          model: model
        ul.append li.render().el
    else
      @disabled = true
      ul.empty()
      (@$ "a").addClass "disabled"

  render: ->
    add = "Filters"

    @root.html """
      <a class="btn dropdown-toggle" href="javascript:void(0)">
        #{ add } <span class="caret"></span>
      </a>
      <ul class="dropdown-menu"></ul>
    """
    @

# An individual list item within the FilterDropdown box
class FilterDropdownItem extends Backbone.View
  tagName: "li"
  events:
    "click a": "onclick"

  initialize: (options) -> {@model} = options
  onclick: ->
    @model.collection.trigger "addFilter",
      model: @model
    @
  render: ->
    @$el.html """
      <a href="javascript:void(0)">#{ @model.get "text" }</a>
    """
    @

# The "Controller" view that bootstraps the filtering controls
# and sets everything in motion.
class FilteringView extends Backbone.View

  initialize: ->
    @filters = new FilterCollection()
    @filters.on "addFilter", (data) => @addFilterEvent data.model
    @filters.on "change", => @checkEmpty()

    @$table = $("div.filter-table")
    @$pool = $("div.filter-fields")
    @$root = $("div.filtering-well")
    @filterDivs = @$pool.find("div.control-group")
    @filterDivs.hide()

    (new FilterDropdown
        root: $ "div.filter-selector"
        filters: @filters
    ).render()

    # Bind the reset button for filters.
    (@$root.find ".btn-reset").on "click", =>
      document.location.search = "?reset" # reset the filters by emptying out the GET
                                          # string and reloading the page.
      for f in @filters.models
        f.set
          cleared: yes
          free: yes


  checkEmpty: ->
    no_filters = "No Filters Selected"
    if @$table.html() is ""
      @$table.append """<h5>#{ no_filters }</h5>"""
    else if (@$table.find ".row-fluid").length > 0
      (@$table.find "h5").remove()

  addFilterEvent: (filter) ->
    @addFilter(filter)
    @$table.find('div.row-fluid').last().find('input').first().focus()

  addFilter: (filter) ->
    filter.set "free", no
    filterView = new FilterWidget
      model: filter
    @$table.append filterView.render().el
    @checkEmpty()

  start: ->
    return @ if typeof (@$table) is "undefined"

    # The pool of fields to draw from
    # takes the items from the pool, and deposits them into models.
    toReAdd = []
    for div in @filterDivs
      div = $ div
      text = div.find("label").text().replace("\n", "")
      id = div.attr("id").replace("\n", "")
      filter = new Filter
        text: text
        selector: id
        baseHtml: div.html()
      @filters.add filter

      valueCarrier = "#" + id.substring(4) # 4 because all filter divs start with "div_"
      valDom = $ valueCarrier

      valid = (value) ->
        return value isnt "" and typeof (value) isnt "undefined" and value isnt null

      val = $(valDom).val()
      if valDom.length is 0
        val0 = $("#{ valueCarrier }_0").val() # in the case that there are multiple elements for
        val1 = $("#{ valueCarrier }_1").val() # the same field (date range, number range, etc)
        val = val0 if valid(val0) and valid(val1)

      toReAdd.push filter if valid(val)

      div.remove() # dispose of the existing div, so we don't have duplicates in the
                   # GET string.

    # re-populare filters if they have existing values.
    @addFilter f for f in toReAdd
    @checkEmpty()
    @


$(document).ready ->
  f = new FilteringView()
  f.start()
