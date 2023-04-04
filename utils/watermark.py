
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class WaterMarkForm(forms.Form):
    image = forms.ImageField("image")


from django.views.generic.edit import FormView
import StringIO
import base64
from PIL import Image, ImageEnhance
from django.conf import settings

class WaterMarkView(LoginRequiredMixin, FormView):
    form_class = WaterMarkForm
    template_name = 'utils/watermark.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            raise Http404()
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                            **kwargs)

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            raise Http404
        context = self.get_context_data()

        output = StringIO.StringIO()

        imag = Image.open(form.cleaned_data['image'])
        watermark = Image.open(settings.STATICFILES_DIRS[0]+'/watermark/cakeglogo.png')

        watermask = watermark.convert("RGBA").point(lambda x: min(x, 100))
        alpha = watermask.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(0.5)

        watermark.putalpha(alpha)

        imageHeight = 1024
        imageWidth = imag.width*imageHeight/imag.height
        imag = imag.resize((imageWidth, imageHeight))
        #imag.thumbnail((imageWidth, imageHeight), Image.ANTIALIAS)
        imag.paste(watermark, (0, 472), watermark)

        imag.save(output, format='PNG')

        output.seek(0)
        output_s = output.read()
        b64 = base64.b64encode(output_s)
        context['base64Image'] = 'data:image/png;base64,{0}'.format(b64)
        output.close()

        return self.render_to_response(context=context)