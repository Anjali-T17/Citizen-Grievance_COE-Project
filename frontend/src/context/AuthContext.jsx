import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('demo_user');
    return saved
      ? JSON.parse(saved)
      : {
          user_id: 'USER_001',
          name: 'Citizen Demo User',
          email: 'citizen@demo.org',
          role: 'Citizen',
          organisation: 'Municipal Corporation',
        };
  });

  const login = async (organisation, role) => {
    try {
      const res = await authAPI.demoLogin(organisation, role);
      setUser(res.data);
      localStorage.setItem('demo_user', JSON.stringify(res.data));
      return res.data;
    } catch (err) {
      console.error('Login error:', err);
      // Fallback
      const fallback = {
        user_id: role === 'Citizen' ? 'USER_001' : role === 'Grievance Officer' ? 'USER_002' : role === 'Supervisor' ? 'USER_003' : 'USER_004',
        name: `Demo ${role}`,
        email: `${role.toLowerCase().replace(' ', '')}@demo.org`,
        role,
        organisation,
      };
      setUser(fallback);
      localStorage.setItem('demo_user', JSON.stringify(fallback));
      return fallback;
    }
  };

  const logout = () => {
    localStorage.removeItem('demo_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
