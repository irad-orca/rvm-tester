# RVM Acceptance Tests

To replicate you can run:

1. Jenkins

   ```shell
   docker run --env JAVA_OPTS="-verbose:class" jenkins/jenkins:lts-jdk17 2>&1 | tee jenkins.log
   python extract.py --type java --log_file jenkins.log > jenkins.txt
   ```

2. JupyterHub

   ```shell
   docker run jupyterhub/jupyterhub:5.2.1 python -v -m jupyterhub 2>&1 | tee jupyterhub.log
   python extract.py --type python --log_file jupyterhub.log > jupyterhub.txt
   ```

3. Posthog

   ```shell
   docker run posthog/posthog:release-1.43.1 python -v manage.py runserver 2>&1 | tee posthog.log
   python extract.py --type python --log_file posthog.log > posthog.txt
   ```

4. Ghost

   ```shell
   docker run -e NODE_DEBUG="module" ghost:5.98.1 node current/index.js 2>&1 | tee ghost.log
   python extract.py --type node --log_file ghost.log > ghost.txt
   ```

5. Strapi

   ```shell
   docker run -e NODE_DEBUG="module" strapi/strapi:3.6.8 strapi develop 2>&1 | tee strapi.log
   python extract.py --type node --log_file strapi.log > strapi.txt
   ```