import { Router } from 'express';
import * as userController from '../controllers/userController';
import { validateUser } from '../validation/userValidation';
import { authMiddleware } from '../middleware/authMiddleware';

const router = Router();

// Apply authMiddleware to all user routes (or specific ones)
router.use(authMiddleware);

router.get('/', userController.getAllUsers);
router.post('/', validateUser, userController.createUser);
router.get('/:id', userController.getUserById);
router.put('/:id', validateUser, userController.updateUser);
router.delete('/:id', userController.deleteUser);

export default router;
