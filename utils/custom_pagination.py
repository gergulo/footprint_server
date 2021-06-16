from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.settings import api_settings
from rest_framework.pagination import PageNumberPagination


def _positive_int(integer_string):
    """
    将一个字符串转成正整数
    """
    ret = int(integer_string)
    if ret <= 0:
        raise ValueError()
    return ret


class CustomPagination(PageNumberPagination):
    """
    自定义分页组件
    """
    # 默认每页记录条数
    page_size = api_settings.PAGE_SIZE
    # 默认页码查询参数名
    page_query_param = "current"
    # 默认默认每页记录条数查询参数名
    page_size_query_param = "size"
    # 默认页码
    page_number = 1
    paginator = None

    def paginate_queryset(self, queryset, request, view=None):
        """
        分页
        :param queryset: 查询模型
        :param request: 请求实例
        :param view: --
        :return: 数据页
        """
        self.page_size = self.get_page_size(request)
        self.page_number = self.get_page_number(request)
        paginator = DjangoPaginator(queryset, self.page_size)
        page = paginator.page(self.page_number)
        self.paginator = paginator
        return list(page)

    def get_page_size(self, request):
        """
        获取获取每页记录条数
        :param request: 请求实例
        :return: 每页记录条数
        """
        if self.page_size_query_param:
            try:
                return _positive_int(request.POST[self.page_size_query_param])
            except (KeyError, ValueError):
                pass
        return self.page_size

    def get_page_number(self, request):
        """
        获取页码
        :param request: 请求实例
        :return: 每页记录条数
        """
        if self.page_query_param:
            try:
                return _positive_int(request.POST[self.page_query_param])
            except (KeyError, ValueError):
                pass
        return self.page_number

    def get_paging_info(self):
        """
        获取分页信息
        :return:
        """
        if self.paginator is None:
            return None
        else:
            return {
                "page_size": self.page_size,
                "current_page": self.page_number,
                "total_count": self.paginator.count,
                "total_pages": self.paginator.num_pages
            }
