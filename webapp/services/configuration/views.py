
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from webapp.models import Configuration
from webapp.shortcuts.ajax import ajax_success, ajax_error


@login_required
def configuration(request, template_name):
    """
    配置 页面
    """
    industry_list = Configuration.objects.values_list('industry', flat=True)
    res = {'industry_list': industry_list}
    return render(request, template_name, res)


@login_required
def configuration_save(request):
    """
    配置 保存数据
    """
    try:
        form_dic = request.POST.dict()
        industry_add = form_dic.get('industry_add')
        industry_delete = form_dic.get('industry_delete')
        if not (industry_add or industry_delete):
            return ajax_error("请输入要保存的数据")
        if industry_add:
            industry_obj = Configuration.objects.filter(industry=industry_add)
            if industry_obj:
                return ajax_error("添加行业已存在")
            else:
                Configuration.objects.create(industry=industry_add)
        if industry_delete:
            Configuration.objects.filter(industry=industry_delete).delete()
        return ajax_success()
    except Exception as e:
        return ajax_error("保存失败")


