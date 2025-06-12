import React, { useState, useEffect } from 'react';

const ProtectedRoute = () => {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProtectedData = async () => {
      try {
        const token = localStorage.getItem('token');
        
        if (!token) {
          setError('No estás autenticado');
          setLoading(false);
          return;
        }

        const response = await fetch(`${process.env.BACKEND_URL}/private`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const data = await response.json();
        
        if (response.ok) {
          setUserData(data);
        } else {
          setError(data.message || 'Acceso no autorizado');
        }
      } catch (error) {
        setError('Error de conexión con el servidor');
      } finally {
        setLoading(false);
      }
    };

    fetchProtectedData();
  }, []);

  if (loading) {
    return <div className="container mt-4">Cargando...</div>;
  }

  if (error) {
    return (
      <div className="container mt-4 alert alert-danger">
        {error}
        <div className="mt-2">
          <a href="/login" className="btn btn-primary">Iniciar Sesión</a>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2>Área Protegida</h2>
      <div className="card">
        <div className="card-body">
          <h5 className="card-title">Bienvenido</h5>
          <p className="card-text">{userData.message}</p>
          <p className="card-text">
            <strong>Email:</strong> {userData.user_email}
          </p>
          <p className="card-text">
            <strong>ID de usuario:</strong> {localStorage.getItem('user_id')}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProtectedRoute;