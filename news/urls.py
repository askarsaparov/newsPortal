from django.urls import path

from news.views import AllNewsPage, AllCategory, homePage, categoryNews, loginPage, logoutUser, \
    registerPage, adminPage, detailNews, adminPageCategoryList, adminPageCategoryDelete, adminCreateCategory, \
    adminUpdateCategory, adminPageCommentsList, adminPageCommentsNewsList, adminPageDeleteComment, \
    adminPageCustomersList, adminPageCustomerDelete, adminPageNewsList, adminPageNewsDelete, adminPageCreateNews, \
    adminPageUpdateNews, profile

urlpatterns = [
    path('', homePage, name='home'),
    path('all_news/', AllNewsPage.as_view(), name='all_news'),
    path('all_category/', AllCategory.as_view(), name='all_category'),
    path('detail/<int:id>/', detailNews, name='detail_news'),
    path('category_news/<int:id>/', categoryNews, name='category_news'),

    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('profile/', profile, name='profile'),

    path('admin2/', adminPage, name='admin'),
    path('admin2/category_list/', adminPageCategoryList, name='admin_page_category_list'),
    path('admin2/category_delete/<int:id>/', adminPageCategoryDelete, name='admin_page_category_delete'),
    path('admin2/category_add/', adminCreateCategory, name='admin_create_category'),
    path('admin2/category_update/<int:id>/', adminUpdateCategory, name='admin_update_category'),
    path('admin2/comment_news_list/', adminPageCommentsNewsList, name='comment_news_list'),
    path('admin2/comments_list/<int:id>/', adminPageCommentsList, name='comments_list'),
    path('admin2/comment_delete/<int:id>/', adminPageDeleteComment, name='comment_delete'),
    path('admin2/customers_list/', adminPageCustomersList, name='customers_list'),
    path('admin2/customers_delete/<int:id>/', adminPageCustomerDelete, name='customer_delete'),
    path('admin2/news_list/', adminPageNewsList, name='admin_news_list'),
    path('admin2/news_delete/<int:id>', adminPageNewsDelete, name='admin_news_delete'),
    path('admin2/news_create/', adminPageCreateNews, name='admin_news_create'),
    path('admin2/news_update/<int:id>', adminPageUpdateNews, name='admin_news_update'),


]