<template>
  <footer
    class="dark:bg-custom-900 bg-custom-100 h-auto w-full text-xs dark:text-custom-500 text-custom-600 cursor-default sm:flex sm:justify-between text-center items-center px-5 py-2 font-medium">
    <p>Theft Prediction System © BSCS 2024. All Rights Reserved.</p>
    <p class="italic">version {{ version }}.{{ commits }}.{{ branchCount }} ({{ branch }})</p>
  </footer>
</template>

<script setup>

const version = ref(3); // Replace with your major version.
const commits = ref(0); // Default commits value.
const branch = ref(''); // Default branch name.
const branchCount = ref(0); // Count of branches.

const getTotalCommits = async () => {
  let page = 1;
  let totalCommits = 0;
  const perPage = 100; // Maximum allowed by GitHub API per page.

  try {
    while (true) {
      const response = await fetch(
        `https://api.github.com/repos/KJLEscoto/Theft-Prediction-System/commits?per_page=${perPage}&page=${page}`
      );

      if (response.ok) {
        const commitData = await response.json();
        totalCommits += commitData.length;

        if (commitData.length < perPage) break; // Exit if there are no more commits.
        page++;
      } else {
        console.error('Error fetching commits:', response.status, response.statusText);
        break;
      }
    }

    commits.value = totalCommits;
  } catch (error) {
    console.error("Error fetching commits count:", error);
  }
};

const getBranchDetails = async () => {
  try {
    const response = await fetch(
      'https://api.github.com/repos/KJLEscoto/Theft-Prediction-System/branches'
    );

    if (response.ok) {
      const branchData = await response.json();
      branchCount.value = branchData.length; // Count of branches
      const defaultBranch = branchData.find(b => b.name === 'main' || b.name === 'master') || branchData[0];
      branch.value = defaultBranch.name;
    } else {
      console.error('Error fetching branches:', response.status, response.statusText);
    }
  } catch (error) {
    console.error("Error fetching branch details:", error);
  }
};

onMounted(() => {
  getTotalCommits();
  getBranchDetails();
});
</script>
