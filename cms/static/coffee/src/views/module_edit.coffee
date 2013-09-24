class CMS.Views.ModuleEdit extends Backbone.View
  tagName: 'li'
  className: 'component'
  editorMode: 'editor-mode'

  events:
    "click .component-editor .cancel-button": 'clickCancelButton'
    "click .component-editor .save-button": 'clickSaveButton'
    "click .component-actions .edit-button": 'clickEditButton'
    "click .component-actions .insert-button": 'clickInsertButton'
    "click .component-actions .insert-to-end-button": 'clickInsertToEndButton'
    "click .component-actions .delete-button": 'onDelete'
    "click .mode a": 'clickModeButton'

  initialize: ->
    @onDelete = @options.onDelete
    @createItemStatus = 0
    @render()

  $component_editor: => @$el.find('.component-editor')

  loadDisplay: ->
    XModule.loadModule(@$el.find('.xmodule_display'))

  loadEdit: ->
    if not @module
      @module = XModule.loadModule(@$el.find('.xmodule_edit'))
      # At this point, metadata-edit.html will be loaded, and the metadata (as JSON) is available.
      metadataEditor = @$el.find('.metadata_edit')
      metadataData = metadataEditor.data('metadata')
      models = [];
      for key of metadataData
        models.push(metadataData[key])
      @metadataEditor = new CMS.Views.Metadata.Editor({
          el: metadataEditor,
          collection: new CMS.Models.MetadataCollection(models)
          })

      # Need to update set "active" class on data editor if there is one.
      # If we are only showing settings, hide the data editor controls and update settings accordingly.
      if @hasDataEditor()
        @selectMode(@editorMode)
      else
        @hideDataEditor()

      title = interpolate(gettext('<em>Редактируется:</em> %s'),
        [@metadataEditor.getDisplayName()])
      @$el.find('.component-name').html(title)

  customMetadata: ->
      # Hack to support metadata fields that aren't part of the metadata editor (ie, LaTeX high level source).
      # Walk through the set of elements which have the 'data-metadata_name' attribute and
      # build up an object to pass back to the server on the subsequent POST.
      # Note that these values will always be sent back on POST, even if they did not actually change.
      _metadata = {}
      _metadata[$(el).data("metadata-name")] = el.value for el in $('[data-metadata-name]',  @$component_editor())
      return _metadata

  changedMetadata: ->
    return _.extend(@metadataEditor.getModifiedMetadataValues(), @customMetadata())

  createItem: (parent, payload) ->
    payload.parent_location = parent
    @createItemStatus = 1
    $.post(
        "/create_item"
        payload 
        (data) => 
            @model.set(id: data.id)
            @$el.data('id', data.id)
            @render()
    )

  render: ->
    if @model.id
      @$el.load("/preview_component/#{@model.id}", =>
        # alert "#{@model.id}"
        @loadDisplay()
        @delegateEvents()
        if @createItemStatus == 1
          @createItemStatus = 0
          @$el.addClass('editing')
          $modalCover.show().addClass('is-fixed')
          @$component_editor().slideDown(150)
          @loadEdit()
      )


  clickSaveButton: (event) =>
    event.preventDefault()
    data = @module.save()

    analytics.track "Saved Module",
      course: course_location_analytics
      id: _this.model.id

    data.metadata = _.extend(data.metadata || {}, @changedMetadata())
    @hideModal()
    saving = new CMS.Views.Notification.Mini
      title: gettext('Сохраняется') + '&hellip;'
    saving.show()
    @model.save(data).done( =>
    #   # showToastMessage("Your changes have been saved.", null, 3)
      @module = null
      @render()
      @$el.removeClass('editing')
      saving.hide()
    ).fail( ->
      showToastMessage(gettext("Возникли проблемы при сохранении. Попробуйте ещё раз"), null, 3)
    )

  clickCancelButton: (event) ->
    event.preventDefault()
    @$el.removeClass('editing')
    @$component_editor().slideUp(150)
    @hideModal()

  hideModal: ->
    $modalCover.hide()
    $modalCover.removeClass('is-fixed')

  clickEditButton: (event) ->
    event.preventDefault()
    @$el.addClass('editing')
    console.log(@$el)
    $modalCover.show().addClass('is-fixed')
    @$component_editor().slideDown(150)
    @loadEdit()

  clickInsertButton: (event) ->
    event.preventDefault()
    vidtime = @$el.find('.vidtime')
    time_str = vidtime.html()
    cur_time_str = time_str.substr(0,time_str.indexOf('/')-1)
    duration_time_str = time_str.substr(time_str.indexOf('/')+2)
    console.log(cur_time_str)
    console.log(duration_time_str)
    cur_time_str_parts = cur_time_str.split(':')
    time = 0
    for elem in cur_time_str_parts
      time_part = parseInt(elem)
      time = time*60+time_part
    console.log(time)
    if time > 0
      if cur_time_str == duration_time_str
        time = time-1
    seconds = time%60
    minutes = ((time-seconds)/60)%60
    hours = (time-minutes*60-seconds)/3600
    seconds_str = seconds + ""
    if seconds_str.length == 1
      seconds_str = "0" + seconds_str
    minutes_str = minutes + ""
    if minutes_str.length == 1
      minutes_str = "0" + minutes_str
    hours_str = hours + ""
    if hours_str.length == 1
      hours_str = "0" + hours_str
    time_format = hours_str + ":" + minutes_str + ":" + seconds_str
    console.log(time_format)
    new_component = document.getElementsByClassName('multiple-templates')
    for elem in new_component
      if elem.getAttribute('data-type') == 'problem'
      #if elem.data.type == 'problem'
        elem.click()
        elem.setAttribute 'time', time_format
        elem.setAttribute 'show_now', 'False'

  clickInsertToEndButton: (event) ->
    event.preventDefault()
    vidtime = @$el.find('.vidtime')
    time_str = vidtime.html()
    duration_time_str = time_str.substr(time_str.indexOf('/')+2)
    console.log(duration_time_str)
    duration_time_str = duration_time_str.split(':')
    time = 0
    for elem in duration_time_str
      time_part = parseInt(elem)
      time = time*60+time_part
    console.log(time)
    if time == 0
      alert "Видео ещё не проигрывается, пожалуйста, нажмите кнопку Play"
    else
      time = time-1
      seconds = time%60
      minutes = ((time-seconds)/60)%60
      hours = (time-minutes*60-seconds)/3600
      seconds_str = seconds + ""
      if seconds_str.length == 1
        seconds_str = "0" + seconds_str
      minutes_str = minutes + ""
      if minutes_str.length == 1
        minutes_str = "0" + minutes_str
      hours_str = hours + ""
      if hours_str.length == 1
        hours_str = "0" + hours_str
      time_format = hours_str + ":" + minutes_str + ":" + seconds_str
      console.log(time_format)
      new_component = document.getElementsByClassName('multiple-templates')
      for elem in new_component
        if elem.getAttribute('data-type') == 'problem'
        #if elem.data.type == 'problem'
          elem.click()
          elem.setAttribute 'time', time_format
          elem.setAttribute 'show_now', 'False'


  clickModeButton: (event) ->
    event.preventDefault()
    if not @hasDataEditor()
      return
    @selectMode(event.currentTarget.parentElement.id)

  hasDataEditor: =>
    return @$el.find('.wrapper-comp-editor').length > 0

  selectMode: (mode) =>
    dataEditor = @$el.find('.wrapper-comp-editor')
    settingsEditor = @$el.find('.wrapper-comp-settings')
    editorModeButton =  @$el.find('#editor-mode').find("a")
    settingsModeButton = @$el.find('#settings-mode').find("a")

    if mode == @editorMode
      # Because of CodeMirror editor, cannot hide the data editor when it is first loaded. Therefore
      # we have to use a class of is-inactive instead of is-active.
      dataEditor.removeClass('is-inactive')
      editorModeButton.addClass('is-set')
      settingsEditor.removeClass('is-active')
      settingsModeButton.removeClass('is-set')
    else
      dataEditor.addClass('is-inactive')
      editorModeButton.removeClass('is-set')
      settingsEditor.addClass('is-active')
      settingsModeButton.addClass('is-set')

  hideDataEditor: =>
    editorModeButtonParent =  @$el.find('#editor-mode')
    editorModeButtonParent.addClass('inactive-mode')
    editorModeButtonParent.removeClass('active-mode')
    @$el.find('.wrapper-comp-settings').addClass('is-active')
    @$el.find('#settings-mode').find("a").addClass('is-set')
