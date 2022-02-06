import axios from 'axios';

export default {

  getGoalsAndSplits() {
    return axios.get('/goalsAndSplits')
  }

}
