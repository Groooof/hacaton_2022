const sign_in_url = '/api/v1/signup';
const log_in_url = '/api/v1/login'

forms = new Vue(
{
	el: '.wrap-login100',
	data: {
		is_new: true,
		log: "",
		pas: "",
		info: ""
	},
	methods: 
	{
		ChangeWindow()
		{
			this.log = "";
			this.pas = "";
			this.info = "";
			this.is_new = !this.is_new;
			
		},
		
		SignUp(event) 
		{
			axios(
			{
				'url': sign_in_url,
				'method': 'post',
				'data': 
				{
					'username': this.log,
					'password': this.pas
				},
				'config': 
				{
					'headers': 
					{
						'Content/Type': 'application/json',

					}
				}
			})
			.then(response => 
			{
				data = response.data
				if (data.success == true)
				{
					this.is_new = false
					this.CleanFields()
					this.info = "Вы успешно зарегистрировались!"
				}
			})
			.catch(err => 
			{
				data = err.response.data
				if (data.success == false)
				{
					switch(data.err) 
					{
						case 'VALIDATION_ERROR': 
							this.info = 'Пароль должен состоять минимум из 8 символов!'
							break
						case 'USER_EXISTS': 
							this.info = 'Пользователь с таким именем уже существует!'
							break
						default: 
							this.info = 'Неизвестная ошибка, попробуйте ещё раз (' + data.err + ')'
					}
				}
			});
			
			
			
		},
		SignIn(event)
		{
			
			
			
			
		},
		LogIn(event)
		{
			axios(
			{
				'url': log_in_url,
				'method': 'post',
				'data': 
				{
					'username': this.log,
					'password': this.pas
				},
				'config': 
				{
					'headers': 
					{
						'Content/Type': 'application/json',

					}
				}
			})
			.then(response => 
			{
				data = response.data
				if (data.success == true)
				{
					window.location.replace('http://app.hacaton.local:8000')
				}
			})
			.catch(err => 
			{
				data = err.response.data
				if (data.success == false)
				{
					switch(data.err) 
					{
						case 'VALIDATION_ERROR': 
							this.info = 'Неверные данные!'
							break
						case 'WRONG_CREDENTIALS': 
							this.info = 'Неверные данные!'
							break
						default: 
							this.info = 'Неизвестная ошибка, попробуйте ещё раз (' + data.err + ')'
					}
				}
			});
			
			
		}
	
  }

})



