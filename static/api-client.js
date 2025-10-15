/**
 * API Client for Redeployable Value Dashboard Backend
 * Handles all communication with Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class DashboardAPI {
  /**
   * Make a POST request to the API
   */
  async post(endpoint, data) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  /**
   * Make a GET request to the API
   */
  async get(endpoint) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'API request failed');
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  /**
   * Calculate homeowner savings
   */
  async calculateHomeowner(params) {
    return await this.post('/calculate/homeowner', params);
  }

  /**
   * Calculate yearly simulation
   */
  async calculateYearly(params) {
    return await this.post('/calculate/yearly', params);
  }

  /**
   * Calculate REP value
   */
  async calculateREP(params) {
    return await this.post('/calculate/rep', params);
  }

  /**
   * Calculate C&I value
   */
  async calculateCI(params) {
    return await this.post('/calculate/ci', params);
  }

  /**
   * Calculate payback period
   */
  async calculatePayback(params) {
    return await this.post('/calculate/payback', params);
  }

  /**
   * Get summary data
   */
  async getSummaryData() {
    return await this.get('/summary/data');
  }
}

// Export singleton instance
const dashboardAPI = new DashboardAPI();
