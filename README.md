# Models V2
```txt
modelsV2
├── src
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── media
│   │   └── profile_pics
│   │       ├── advisorpic.png
│   │       ├── askar_nurbekov.jpg
│   │       ├── default.png
│   │       ├── emmett-tomai.jpg
│   │       ├── erik_enriquez.jpg
│   │       ├── marzieh-ayati-02.jpg
│   │       └── timothy-wylie.jpg
│   ├── project_manager
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_alter_user_managers.py
│   │   │   ├── 0003_alter_user_email.py
│   │   │   ├── 0004_project_skills_required.py
│   │   │   ├── 0005_project_member_limit.py
│   │   │   ├── 0006_projectapplication.py
│   │   │   ├── 0007_alter_project_advisor_alter_project_created_by.py
│   │   │   ├── 0008_favorite.py
│   │   │   ├── 0009_studentprofile.py
│   │   │   ├── 0010_advisorprofile_image.py
│   │   │   └── __init__.py
│   │   ├── static
│   │   │   └── project_manager
│   │   │       ├── css
│   │   │       │   └── style.css
│   │   │       ├── advisorpic.png
│   │   │       ├── advisor.png
│   │   │       ├── create-project.png
│   │   │       ├── utrgv-logo-orange.png
│   │   │       ├── utrgv-logo.svg
│   │   │       ├── utrgv.svg
│   │   │       └── view-projects.png
│   │   ├── templates
│   │   │   ├── project_manager
│   │   │   │   ├── advisorDetailPage.html
│   │   │   │   ├── advisorListPage.html
│   │   │   │   ├── base.html
│   │   │   │   ├── landingPage.html
│   │   │   │   ├── loginPage.html
│   │   │   │   ├── projectApplicationDetailView.html
│   │   │   │   ├── projectApplicationList.html
│   │   │   │   ├── projectApplicationPage.html
│   │   │   │   ├── projectDetailPage.html
│   │   │   │   ├── projectListPage.html
│   │   │   │   └── projectProposalPage.html
│   │   │   └── static
│   │   │       └── css
│   │   │           └── style.css
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static
│   ├── staticfiles
│   │   ├── admin
│   │   │   ├── css
│   │   │   │   ├── vendor
│   │   │   │   │   └── select2
│   │   │   │   ├── autocomplete.css
│   │   │   │   ├── base.css
│   │   │   │   ├── changelists.css
│   │   │   │   ├── dark_mode.css
│   │   │   │   ├── dashboard.css
│   │   │   │   ├── forms.css
│   │   │   │   ├── login.css
│   │   │   │   ├── nav_sidebar.css
│   │   │   │   ├── responsive.css
│   │   │   │   ├── responsive_rtl.css
│   │   │   │   ├── rtl.css
│   │   │   │   ├── unusable_password_field.css
│   │   │   │   └── widgets.css
│   │   │   ├── img
│   │   │   │   ├── gis
│   │   │   │   │   ├── move_vertex_off.svg
│   │   │   │   │   └── move_vertex_on.svg
│   │   │   │   ├── calendar-icons.svg
│   │   │   │   ├── icon-addlink.svg
│   │   │   │   ├── icon-alert.svg
│   │   │   │   ├── icon-calendar.svg
│   │   │   │   ├── icon-changelink.svg
│   │   │   │   ├── icon-clock.svg
│   │   │   │   ├── icon-deletelink.svg
│   │   │   │   ├── icon-hidelink.svg
│   │   │   │   ├── icon-no.svg
│   │   │   │   ├── icon-unknown-alt.svg
│   │   │   │   ├── icon-unknown.svg
│   │   │   │   ├── icon-viewlink.svg
│   │   │   │   ├── icon-yes.svg
│   │   │   │   ├── inline-delete.svg
│   │   │   │   ├── LICENSE
│   │   │   │   ├── README.txt
│   │   │   │   ├── search.svg
│   │   │   │   ├── selector-icons.svg
│   │   │   │   ├── sorting-icons.svg
│   │   │   │   ├── tooltag-add.svg
│   │   │   │   └── tooltag-arrowright.svg
│   │   │   └── js
│   │   │       ├── admin
│   │   │       │   ├── DateTimeShortcuts.js
│   │   │       │   └── RelatedObjectLookups.js
│   │   │       ├── vendor
│   │   │       │   ├── jquery
│   │   │       │   ├── select2
│   │   │       │   └── xregexp
│   │   │       ├── actions.js
│   │   │       ├── autocomplete.js
│   │   │       ├── calendar.js
│   │   │       ├── cancel.js
│   │   │       ├── change_form.js
│   │   │       ├── core.js
│   │   │       ├── filters.js
│   │   │       ├── inlines.js
│   │   │       ├── jquery.init.js
│   │   │       ├── nav_sidebar.js
│   │   │       ├── popup_response.js
│   │   │       ├── prepopulate_init.js
│   │   │       ├── prepopulate.js
│   │   │       ├── SelectBox.js
│   │   │       ├── SelectFilter2.js
│   │   │       ├── theme.js
│   │   │       ├── unusable_password_field.js
│   │   │       └── urlify.js
│   │   ├── django_select2
│   │   │   ├── django_select2.css
│   │   │   └── django_select2.js
│   │   └── project_manager
│   │       ├── css
│   │       │   └── style.css
│   │       ├── advisorpic.png
│   │       ├── advisor.png
│   │       ├── create-project.png
│   │       ├── utrgv-logo-orange.png
│   │       ├── utrgv-logo.svg
│   │       ├── utrgv.svg
│   │       └── view-projects.png
│   ├── templates
│   │   └── registration
│   │       └── login.html
│   ├── db.sqlite3
│   └── manage.py
├── tests
│   └── __init__.py
├── notes.txt
├── poetry.lock
├── pyproject.toml
└── README.md

34 directories, 126 files

```
