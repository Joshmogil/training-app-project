import axios from 'axios';

export default {

  changeSettings(settings) {
    return axios.post('/settings', settings)
  },

  register(user) {
    return axios.post('/register', user)
  }

}
