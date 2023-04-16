from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):
    """ユーザー登録画面用のフォーム"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
        }
    password2 = forms.CharField(
        label='確認用パスワード',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'}),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'ユーザー名'}
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

    def clean(self):
        # 明示的に親クラスのclean()を呼び出す
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")

class LoginForm(forms.Form):
    """ログイン画面用のフォーム"""
    username = forms.CharField(
        label='ユーザー名',
        max_length=225,
    )

    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(),
    )

    def clean_username(self):
        # 入力値はclean_data から取得
        username = self.cleaned_data['username']
        # 入力値が３桁より短ければバリデーションエラー
        if len(username) < 3:
            raise forms.ValidationError(
                '%(min_length)s文字以上で入力してください',
                code='invalid', params={'min_length': 3})
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            # ユーザー名で検索して検証（平文のパスワードでは検索できない）
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("正しいユーザー名を入力してください")

        # パスワードの検証
        if not user.check_password(password):
            raise forms.ValidationError("正しいパスワードを入力してください")
