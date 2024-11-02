import { getSpecificAvatar } from '~/assets/js/avatar';

export const generateData = (gdata) => {
    return gdata;
};

export const generateActiveData = (gdata) => {
    return gdata;
};

export const generateInactiveData = (gdata) => {
    return gdata;
};

// Define a function to fetch a specific avatar
function fetchSpecificAvatar(index) {
    return getSpecificAvatar(index);  // Call the imported function and return the result
}

export async function fetchUsers() {
    // console.log('Fetching users...');
    try {
        const response = await fetch('http://127.0.0.1:8000/api/users', {
            method: 'GET',
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('_token') // Use 'Bearer' prefix for token
            }
        });
        
        if (!response.ok) {
            throw new Error(`No data found in response: ${response.statusText}`);
        }

        const data = await response.json();
        // console.log('Fetched users data:', data);

        // Ensure we handle multiple users dynamically
        const generate_data = data.map(user => ({
            id: user.id,
            username: user.username,
            avatar: ref(fetchSpecificAvatar(user.avatar)),
            role: user.role,
            status: user.status,
            name: `${user.first_name} ${user.middle_initial ? user.middle_initial + '. ' : ''}${user.last_name}`
        }));

        return generateData(generate_data);

    } catch (error) {
        console.error('Error fetching users:', error.message);
    }
}



export async function fetchActiveUsers() {
    // console.log('Fetching users...');
    try {
        const response = await fetch('http://127.0.0.1:8000/api/active', {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error(`No data found in response: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Fetched active users data:', data);

        // Ensure we handle multiple users dynamically
        const generate_active_data = data.map(user => ({
            id: user.id,
            username: user.username,
            avatar: ref(fetchSpecificAvatar(user.avatar)),
            role: user.role,
            status: user.status,
            name: `${user.first_name} ${user.middle_initial ? user.middle_initial + '. ' : ''}${user.last_name}`
        }));

        return generateActiveData(generate_active_data);

    } catch (error) {
        console.error('Error fetching users:', error.message);
    }
}



export async function fetchInactiveUsers() {
    // console.log('Fetching users...');
    try {
        const response = await fetch('http://127.0.0.1:8000/api/inactive', {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error(`No data found in response: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Fetched inactive users data:', data);

        // Ensure we handle multiple users dynamically
        const generate_inactive_data = data.map(user => ({
            id: user.id,
            username: user.username,
            avatar: ref(fetchSpecificAvatar(user.avatar)),
            role: user.role,
            status: user.status,
            name: `${user.first_name} ${user.middle_initial ? user.middle_initial + '. ' : ''}${user.last_name}`
        }));

        return generateInactiveData(generate_inactive_data);

    } catch (error) {
        console.error('Error fetching users:', error.message);
    }
}
