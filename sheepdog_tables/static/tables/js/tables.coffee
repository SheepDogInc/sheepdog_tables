class Column
    ###
    #   Column is meant to be similar to that of the python API.
    #   The primary difference to note is how the HTML is generated.  Everything
    #   is generated via Underscore's template builder.  Thus, each column
    #   should supply a template string to utilize.
    #
    #   :params
    #   field -- the field to act on, set by the table.
    ###
    field: null
    template_string: "<td><%= data =></td>" 

    constructor: (options) ->
        @options = options

    header: ->
        field = @options?.field or @field
        field[0] = field[0].toUpperCase()
        @options?.header or field

    template: ->
        _.template(@template_string)

    render: (data) ->
        (do @template) data

class Table
    ###
    #   Table API
    #   This is supposed to partially mimic the sheepdog_tables python API
    #
    #   :params
    #   table_sequence -- the explicit order columns should be rendered in
    ###
    table_sequence: null

    constructor: ->
        for col in @table_sequence
            @[col].field = col if not @[col].options.field?
        @
    
    get_headers: ->
        (@[col].header() for col in @table_sequence)



Tables.Utils.namespace 'Tables', (exports) ->
    exports.Table = Table
    exports.Column = Column

